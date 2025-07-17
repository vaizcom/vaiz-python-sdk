import { ClientOptions } from './types';
import { TasksAPIClient } from './tasks';
import { ProjectsAPIClient } from './projects';
import { BoardsAPIClient } from './boards';
import { ProfileAPIClient } from './profile';
import { MilestonesAPIClient } from './milestones';
import { UploadAPIClient } from './upload';
import { CommentsAPIClient } from './comments';

export class VaizClient extends TasksAPIClient {
  public projects: ProjectsAPIClient;
  public boards: BoardsAPIClient;
  public profile: ProfileAPIClient;
  public milestones: MilestonesAPIClient;
  public upload: UploadAPIClient;
  public comments: CommentsAPIClient;

  constructor(options: ClientOptions) {
    super(options);
    
    // Initialize all API clients with the same options
    this.projects = new ProjectsAPIClient(options);
    this.boards = new BoardsAPIClient(options);
    this.profile = new ProfileAPIClient(options);
    this.milestones = new MilestonesAPIClient(options);
    this.upload = new UploadAPIClient(options);
    this.comments = new CommentsAPIClient(options);
  }

  // Convenience methods that delegate to the upload client
  async uploadFile(filePath: string, fileType: any) {
    return this.upload.uploadFile(filePath, fileType);
  }

  async uploadFileFromFile(file: File, fileType: any) {
    return this.upload.uploadFileFromFile(file, fileType);
  }
}