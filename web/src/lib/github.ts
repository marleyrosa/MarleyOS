export const GITHUB_REPO = "vudovn/ag-kit";
export const GITHUB_REPO_URL = `https://github.com/${GITHUB_REPO}`;
export const GITHUB_API_URL = `https://api.github.com/repos/${GITHUB_REPO}`;
export const GITHUB_CONTRIBUTORS_URL = `${GITHUB_API_URL}/contributors?per_page=100`;

const CACHE_TTL_MS = 60_000;

type StarsCache = {
  stars: number;
  fetchedAt: number;
};

export type GithubContributor = {
  login: string;
  avatarUrl: string;
  htmlUrl: string;
  contributions: number;
};

type ContributorsCache = {
  contributors: GithubContributor[];
  fetchedAt: number;
};

let memoryCache: StarsCache | null = null;
let inflight: Promise<number | null> | null = null;
let contributorsCache: ContributorsCache | null = null;
let contributorsInflight: Promise<GithubContributor[]> | null = null;

/** Format star counts for compact button labels (e.g. 1240 → 1.2k). */
export function formatStarCount(count: number): string {
  if (count < 1000) return String(count);
  if (count < 10_000) {
    const value = (count / 1000).toFixed(1);
    return `${value.endsWith(".0") ? value.slice(0, -2) : value}k`;
  }
  if (count < 1_000_000) return `${Math.round(count / 1000)}k`;
  return `${(count / 1_000_000).toFixed(1).replace(/\.0$/, "")}m`;
}

/**
 * Fetch stargazers_count for the AG Kit repo.
 * Dedupes concurrent requests and caches for 60s (client or server).
 */
export async function fetchGithubStars(): Promise<number | null> {
  if (memoryCache && Date.now() - memoryCache.fetchedAt < CACHE_TTL_MS) {
    return memoryCache.stars;
  }

  if (inflight) return inflight;

  inflight = (async () => {
    try {
      const response = await fetch(GITHUB_API_URL, {
        headers: {
          Accept: "application/vnd.github+json",
          "User-Agent": "ag-kit-web",
        },
        // Next.js server cache; ignored in the browser.
        next: { revalidate: 60 },
      });

      if (!response.ok) return memoryCache?.stars ?? null;

      const data = (await response.json()) as { stargazers_count?: number };
      const stars = data.stargazers_count;
      if (typeof stars !== "number" || !Number.isFinite(stars)) {
        return memoryCache?.stars ?? null;
      }

      memoryCache = { stars, fetchedAt: Date.now() };
      return stars;
    } catch {
      return memoryCache?.stars ?? null;
    } finally {
      inflight = null;
    }
  })();

  return inflight;
}

/**
 * Fetch public contributors for the AG Kit repo (sorted by contributions).
 * Cached 60s; concurrent callers share one request.
 */
export async function fetchGithubContributors(): Promise<GithubContributor[]> {
  if (
    contributorsCache &&
    Date.now() - contributorsCache.fetchedAt < CACHE_TTL_MS
  ) {
    return contributorsCache.contributors;
  }

  if (contributorsInflight) return contributorsInflight;

  contributorsInflight = (async () => {
    try {
      const response = await fetch(GITHUB_CONTRIBUTORS_URL, {
        headers: {
          Accept: "application/vnd.github+json",
          "User-Agent": "ag-kit-web",
        },
        next: { revalidate: 60 },
      });

      if (!response.ok) return contributorsCache?.contributors ?? [];

      const data = (await response.json()) as Array<{
        login?: string;
        avatar_url?: string;
        html_url?: string;
        contributions?: number;
        type?: string;
      }>;

      if (!Array.isArray(data)) return contributorsCache?.contributors ?? [];

      const contributors = data
        .filter(
          (item) =>
            item.type !== "Bot" &&
            typeof item.login === "string" &&
            typeof item.avatar_url === "string" &&
            typeof item.html_url === "string",
        )
        .map((item) => ({
          login: item.login as string,
          avatarUrl: item.avatar_url as string,
          htmlUrl: item.html_url as string,
          contributions:
            typeof item.contributions === "number" ? item.contributions : 0,
        }));

      contributorsCache = { contributors, fetchedAt: Date.now() };
      return contributors;
    } catch {
      return contributorsCache?.contributors ?? [];
    } finally {
      contributorsInflight = null;
    }
  })();

  return contributorsInflight;
}
