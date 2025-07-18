import { TasksAPIClient } from './tasks';
import { ProjectsAPIClient } from './projects';
import { ClientOptions } from './base';

export class VaizClient extends TasksAPIClient {
  projects: ProjectsAPIClient;

  constructor(options: ClientOptions) {
    super(options);
    this.projects = new ProjectsAPIClient(options);
  }
}

export * from './tasks';
export * from './projects';
export * from './base';
