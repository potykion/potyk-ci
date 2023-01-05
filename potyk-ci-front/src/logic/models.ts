export const JobStatuses = {DONE: 'DONE', ERR: 'ERR', PENDING: 'PENDING', CANCELLED: 'CANCELLED'} as const;
export type JobStatus = keyof typeof JobStatuses;


export interface Job {
    status: JobStatus;
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