export interface ManuscriptState {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  totalWords: number;
  totalEquations: number;
  totalFigures: number;
  sectionsCount: number;
  sections: Array<{
    id: string;
    title: string;
    paragraphs: number;
    equations: string[];
    completeness: number; // 0 - 100%
  }>;
  coreEquations: Array<{
    name: string;
    latex: string;
    description: string;
  }>;
  algorithms: Array<{
    name: string;
    language: "python" | "cpp" | "matlab";
    code: string;
    targetModule: string;
  }>;
  hilBenchmarks: {
    platform: "dSPACE SCALEXIO" | "ETAS LABCAR";
    samplingRateKhz: number;
    rmseErrorPercent: number;
    maxJitterMicroseconds: number;
    correlationFactor: number; // 0 - 1
    sampleSignals: Array<{
      timeMs: number;
      actualCurrent: number;
      estimatedCurrent: number;
      error: number;
    }>;
  };
}

export const KIOTOPAPER_MANUSCRIPT: ManuscriptState = {
  id: "kioto-paper-01",
  title: "Real-Time Embedded Model-Based Control & Hardware-in-the-Loop Validation for High-Efficiency Electric Powertrains",
  authors: ["Kiotopaper Research Lab", "Automotive Systems Group"],
  abstract:
    "This work presents a high-bandwidth model-based control framework coupled with an Extended Kalman Filter (EKF) observer for next-generation electric traction inverters. The synthesis encompasses state estimation under high-frequency switching harmonics, verified across Model-in-the-Loop (MIL), Software-in-the-Loop (SIL), and executed on a dSPACE SCALEXIO Hardware-in-the-Loop (HIL) automotive testbed with microsecond timing determinism.",
  totalWords: 7420,
  totalEquations: 28,
  totalFigures: 14,
  sectionsCount: 7,
  sections: [
    {
      id: "sec-1",
      title: "1. Introduction & Electrification State-of-the-Art",
      paragraphs: 6,
      equations: [],
      completeness: 100,
    },
    {
      id: "sec-2",
      title: "2. Powertrain Electromechanical Dynamics & State Space",
      paragraphs: 8,
      equations: [
        "\\dot{x}(t) = A x(t) + B u(t) + G w(t)",
        "y(t) = C x(t) + D u(t) + v(t)",
      ],
      completeness: 100,
    },
    {
      id: "sec-3",
      title: "3. Non-linear Observer Synthesis (Extended Kalman Filter)",
      paragraphs: 10,
      equations: [
        "\\hat{x}_{k|k-1} = f(\\hat{x}_{k-1|k-1}, u_{k-1})",
        "P_{k|k-1} = F_{k-1} P_{k-1|k-1} F_{k-1}^T + Q_{k-1}",
        "K_k = P_{k|k-1} H_k^T (H_k P_{k|k-1} H_k^T + R_k)^{-1}",
      ],
      completeness: 95,
    },
    {
      id: "sec-4",
      title: "4. Model Predictive Current Controller (MPCC)",
      paragraphs: 9,
      equations: [
        "J = \\sum_{j=1}^{N_p} \\| y_{k+j} - r_{k+j} \\|_{Q}^2 + \\sum_{j=0}^{N_c-1} \\| \\Delta u_{k+j} \\|_{R}^2",
      ],
      completeness: 90,
    },
    {
      id: "sec-5",
      title: "5. XIL Emulation Pipeline (MIL -> SIL -> HIL Bench)",
      paragraphs: 7,
      equations: [
        "\\epsilon_{\\text{HIL}}(t) = | i_{\\text{bench}}(t) - i_{\\text{sim}}(t) | \\le \\delta_{\\text{thresh}}",
      ],
      completeness: 100,
    },
    {
      id: "sec-6",
      title: "6. Experimental Results & Hardware Benchmarking",
      paragraphs: 11,
      equations: [],
      completeness: 85,
    },
    {
      id: "sec-7",
      title: "7. Conclusion & Journal Compliance Synthesis",
      paragraphs: 4,
      equations: [],
      completeness: 80,
    },
  ],
  coreEquations: [
    {
      name: "Nonlinear Powertrain Dynamics",
      latex: "\\frac{d}{dt} \\begin{bmatrix} i_d \\\\ i_q \\\\ \\omega_r \\end{bmatrix} = \\begin{bmatrix} -\\frac{R_s}{L_d} i_d + \\frac{L_q}{L_d} p \\omega_r i_q + \\frac{v_d}{L_d} \\\\ -\\frac{R_s}{L_q} i_q - \\frac{L_d}{L_q} p \\omega_r i_d - \\frac{\\lambda_{pm} p \\omega_r}{L_q} + \\frac{v_q}{L_q} \\\\ \\frac{3 p}{2 J} [\\lambda_{pm} i_q + (L_d - L_q) i_d i_q] - \\frac{T_L}{J} - \\frac{B \\omega_r}{J} \\end{bmatrix}",
      description: "PMSM synchronous reference frame DQ state evolution coupled with mechanical inertia.",
    },
    {
      name: "Kalman Innovation Gain",
      latex: "K_k = P_{k|k-1} H_k^T \\left( H_k P_{k|k-1} H_k^T + R_k \\right)^{-1}",
      description: "Optimal gain matrix balancing model covariance P and sensor noise R.",
    },
    {
      name: "Lyapunov Candidate for MPCC Stability",
      latex: "V(x) = x^T P x > 0, \\quad \\Delta V(x) = x_{k+1}^T P x_{k+1} - x_k^T P x_k \\le - x_k^T Q^* x_k",
      description: "Asymptotic stability condition ensuring convergent current trajectories under voltage limits.",
    },
  ],
  algorithms: [
    {
      name: "Discrete EKF State Observer",
      language: "python",
      targetModule: "AG-01 / AG-03 Method Validator",
      code: `import numpy as np

class ExtendedKalmanFilter:
    def __init__(self, dt: float, Rs: float, Ld: float, Lq: float, psi_pm: float):
        self.dt = dt
        self.Rs, self.Ld, self.Lq, self.psi = Rs, Ld, Lq, psi_pm
        self.x = np.zeros((3, 1)) # [id, iq, omega]
        self.P = np.eye(3) * 0.05
        self.Q = np.diag([1e-3, 1e-3, 1e-2])
        self.R = np.diag([0.02, 0.02])

    def predict(self, u_dq: np.ndarray):
        id_curr, iq_curr, w_curr = self.x.ravel()
        did = (-self.Rs/self.Ld * id_curr + self.Lq/self.Ld * w_curr * iq_curr + u_dq[0]/self.Ld) * self.dt
        diq = (-self.Rs/self.Lq * iq_curr - self.Ld/self.Lq * w_curr * id_curr - self.psi*w_curr/self.Lq + u_dq[1]/self.Lq) * self.dt
        self.x[0] += did
        self.x[1] += diq
        # Jacobian F evaluation
        F = np.array([
            [1.0 - (self.Rs/self.Ld)*self.dt, (self.Lq/self.Ld)*w_curr*self.dt, (self.Lq/self.Ld)*iq_curr*self.dt],
            [-(self.Ld/self.Lq)*w_curr*self.dt, 1.0 - (self.Rs/self.Lq)*self.dt, -(self.Ld/self.Lq*id_curr + self.psi/self.Lq)*self.dt],
            [0.0, 0.0, 1.0]
        ])
        self.P = F @ self.P @ F.T + self.Q
        return self.x

    def update(self, z_meas: np.ndarray):
        H = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
        y = z_meas.reshape((2,1)) - H @ self.x
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x += K @ y
        self.P = (np.eye(3) - K @ H) @ self.P
        return self.x`,
    },
  ],
  hilBenchmarks: {
    platform: "dSPACE SCALEXIO",
    samplingRateKhz: 20.0,
    rmseErrorPercent: 0.042,
    maxJitterMicroseconds: 0.85,
    correlationFactor: 0.994,
    sampleSignals: [
      { timeMs: 0.0, actualCurrent: 12.0, estimatedCurrent: 12.05, error: -0.05 },
      { timeMs: 1.0, actualCurrent: 35.2, estimatedCurrent: 35.12, error: 0.08 },
      { timeMs: 2.0, actualCurrent: 68.7, estimatedCurrent: 68.80, error: -0.10 },
      { timeMs: 3.0, actualCurrent: 94.3, estimatedCurrent: 94.18, error: 0.12 },
      { timeMs: 4.0, actualCurrent: 110.0, estimatedCurrent: 109.95, error: 0.05 },
      { timeMs: 5.0, actualCurrent: 112.5, estimatedCurrent: 112.60, error: -0.10 },
      { timeMs: 6.0, actualCurrent: 108.0, estimatedCurrent: 107.92, error: 0.08 },
      { timeMs: 7.0, actualCurrent: 92.4, estimatedCurrent: 92.30, error: 0.10 },
    ],
  },
};
