// ============================================
// Types per Dashboard MAPPA CervellaSwarm
// ============================================

// IL NORD - Obiettivo del progetto
export interface Nord {
  obiettivo: string;
  descrizione: string;
  progressoGenerale: number; // 0-100
  sessioneCorrente: number;
  frase?: string; // Frase motivazionale
}

// LA FAMIGLIA - I 16 agenti
export type WorkerStatus = 'idle' | 'working' | 'done' | 'error';
export type WorkerModel = 'opus' | 'sonnet';

export interface Worker {
  id: string;
  nome: string;
  emoji: string;
  descrizione: string;
  model: WorkerModel;
  status: WorkerStatus;
  taskCorrente?: string;
  ultimoTask?: string;
  ultimoTaskTimestamp?: string;
}

export interface Famiglia {
  regina: Worker;
  guardiane: Worker[];
  workers: Worker[];
  attiviCount: number;
  idleCount: number;
}

// LA ROADMAP - Step del progetto
export type StepStatus = 'completed' | 'in_progress' | 'pending';

export interface SubStep {
  id: string;
  titolo: string;
  status: StepStatus;
  descrizione?: string;
}

export interface Step {
  id: string;
  numero: number;
  titolo: string;
  descrizione: string;
  status: StepStatus;
  progresso: number; // 0-100
  subSteps: SubStep[];
}

export interface Roadmap {
  steps: Step[];
  stepCorrente: number;
  progressoTotale: number;
}

// SESSIONE ATTIVA
export interface LogMessage {
  timestamp: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
}

export interface SessioneAttiva {
  taskId?: string;
  taskNome?: string;
  workerAssegnato?: string;
  inizioTimestamp?: string;
  durataSecondi: number;
  outputFile?: string;
  logs: LogMessage[];
  isActive: boolean;
}

// API Response types
export interface DashboardData {
  nord: Nord;
  famiglia: Famiglia;
  roadmap: Roadmap;
  sessione: SessioneAttiva;
  lastUpdate: string;
}

// SSE Event types
export type SSEEventType =
  | 'nord_update'
  | 'famiglia_update'
  | 'roadmap_update'
  | 'sessione_update'
  | 'task_started'
  | 'task_completed'
  | 'heartbeat';

export interface SSEEvent {
  type: SSEEventType;
  data: Partial<DashboardData>;
  timestamp: string;
}
