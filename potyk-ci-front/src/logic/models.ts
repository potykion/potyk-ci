export interface QAJob {
  success: boolean;
  output: string;
  created: string;
  id: number;
}

export interface Project {
  path: string;
  command: string;
  id: number;
  name: string;

}