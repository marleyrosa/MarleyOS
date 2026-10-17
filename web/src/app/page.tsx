import {
  LandingBenefits,
  LandingContribute,
  LandingFAQ,
  LandingFeatures,
  LandingFooter,
  LandingHero,
  LandingNavbar,
  LandingSponsored,
  LandingSponsors,
  LandingTestimonials,
  LandingWorkflows,
} from "@/components/landing";

export default function Home() {
  return (
    <div className="min-h-[100dvh] bg-background overflow-x-hidden">
      <LandingNavbar />
      <main id="main-content" tabIndex={-1}>
        <LandingHero />
        <LandingSponsors />
        <LandingBenefits />
        <LandingFeatures />
        <LandingWorkflows />
        <LandingTestimonials />
        <LandingSponsored />
        <LandingContribute />
        <LandingFAQ />
      </main>
      <LandingFooter />
    </div>
  );
}
