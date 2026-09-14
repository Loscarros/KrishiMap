import { api } from "@/lib/api";
import { FarmTask } from "@/types/calendar";

interface BackendFarmTask {
  id: number;
  farm_id: number;
  title: string;
  description: string;
  date: string;
  type: FarmTask["type"];
  status: FarmTask["status"];
  created_at: string;
  updated_at: string;
}

function normalizeTask(
  task: BackendFarmTask
): FarmTask {
  return {
    id: String(task.id),
    title: task.title,
    description: task.description,
    date: task.date,
    type: task.type,
    status: task.status,
  };
}


export async function getFarmTasks(
  farmId: string
): Promise<FarmTask[]> {
  const response =
    await api.get<BackendFarmTask[]>(
      `/farms/${farmId}/tasks`
    );

  return response.data.map(
    normalizeTask
  );
}


export async function createFarmTask(
  farmId: string,
  task: Omit<FarmTask, "id">
): Promise<FarmTask> {
  const response =
    await api.post<BackendFarmTask>(
      `/farms/${farmId}/tasks`,
      task
    );

  return normalizeTask(
    response.data
  );
}


export async function updateFarmTask(
  farmId: string,
  taskId: string,
  updates: Partial<FarmTask>
): Promise<FarmTask> {
  const response =
    await api.patch<BackendFarmTask>(
      `/farms/${farmId}/tasks/${taskId}`,
      updates
    );

  return normalizeTask(
    response.data
  );
}


export async function deleteFarmTask(
  farmId: string,
  taskId: string
): Promise<void> {
  await api.delete(
    `/farms/${farmId}/tasks/${taskId}`
  );
}