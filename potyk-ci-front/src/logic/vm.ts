import {JobStatuses} from "@/logic/models";
import type {JobStatus, Job} from "@/logic/models";

export class JobVM {
    status: JobStatus;
    output: string;
    created: string;
    id: number;

    constructor(job: Job) {
        this.status = job.status;
        this.output = job.output;
        this.created = job.created;
        this.id = job.id;
    }

    get statusColor() {
        switch (this.status) {
            case JobStatuses.DONE:
                return 'text-green-400';
            case "ERR":
                return 'text-red-400'
            case "PENDING":
                return 'text-amber-400';
            case "CANCELLED":
                return 'text-gray-500';
        }
    }

}