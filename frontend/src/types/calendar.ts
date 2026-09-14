export type TaskStatus =
  | "pending"
  | "completed"
  | "postponed";


export type FarmTaskType =
  | "irrigation"
  | "fertilizer"
  | "monitoring"
  | "harvest"
  | "other";


export interface FarmTask {
  id: string;
  title: string;
  description: string;
  date: string;
  type: FarmTaskType;
  status: TaskStatus;
}