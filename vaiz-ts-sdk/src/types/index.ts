// Enums
export enum TaskPriority {
  Low = 'Low',
  Medium = 'Medium', 
  High = 'High',
  Critical = 'Critical'
}

export enum EUploadFileType {
  Image = 'Image',
  Video = 'Video',
  Pdf = 'Pdf',
  File = 'File'
}

export enum CommentReactionType {
  ThumbsUp = 'thumbsup',
  ThumbsDown = 'thumbsdown',
  Heart = 'heart',
  Laugh = 'laugh',
  Surprised = 'surprised',
  Sad = 'sad',
  Angry = 'angry'
}

export enum CustomFieldType {
  Text = 'Text',
  Number = 'Number',
  Date = 'Date',
  Boolean = 'Boolean',
  Select = 'Select',
  MultiSelect = 'MultiSelect'
}

// Base interfaces
export interface ClientOptions {
  apiKey: string;
  spaceId: string;
  baseUrl?: string;
  verifySsl?: boolean;
  verbose?: boolean;
}

export interface APIError {
  code: string;
  fields?: any[];
  originalType?: string;
  meta?: {
    description?: string;
    token?: string;
  };
}

// Task-related interfaces
export interface TaskFollower {
  id: string;
  name: string;
  avatar?: string;
}

export interface CustomField {
  id: string;
  name: string;
  type: CustomFieldType;
  value: any;
}

export interface TaskFile {
  id: string;
  url: string;
  name: string;
  ext: string;
  type: EUploadFileType;
  dimension?: string;
  size?: number;
}

export interface TaskUploadFile {
  path: string;
  type: EUploadFileType;
}

export interface Task {
  _id: string;
  name: string;
  description?: string;
  completed: boolean;
  priority: TaskPriority;
  assignees: string[];
  followers: TaskFollower[];
  customFields?: CustomField[];
  files?: TaskFile[];
  document?: string;
  dueStart?: Date;
  dueEnd?: Date;
  createdAt?: Date;
  updatedAt?: Date;
  slug?: string;
  project?: string;
  board?: string;
  group?: string;
}

export interface CreateTaskRequest {
  name: string;
  group: string;
  board: string;
  project: string;
  priority?: TaskPriority;
  completed?: boolean;
  description?: string;
  files?: TaskFile[];
  dueStart?: Date;
  dueEnd?: Date;
  assignees?: string[];
  types?: string[];
  subtasks?: string[];
  milestones?: string[];
  rightConnectors?: string[];
  leftConnectors?: string[];
}

export interface EditTaskRequest {
  taskId: string;
  name?: string;
  completed?: boolean;
  priority?: TaskPriority;
  description?: string;
  dueStart?: Date;
  dueEnd?: Date;
  assignees?: string[];
}

export interface TaskResponse {
  type: string;
  payload: {
    task: Task;
  };
  task: Task; // For convenience
}

// Project interfaces
export interface Project {
  _id: string;
  name: string;
  description?: string;
  color?: string;
  archived?: boolean;
  createdAt?: Date;
  updatedAt?: Date;
}

export interface ProjectsResponse {
  type: string;
  payload: {
    projects: Project[];
  };
}

export interface ProjectResponse {
  type: string;
  payload: {
    project: Project;
  };
}

// Board interfaces
export interface BoardType {
  id: string;
  label: string;
  icon: string;
  color: string | EColor;
}

export enum EColor {
  Red = 'red',
  Blue = 'blue',
  Green = 'green',
  Yellow = 'yellow',
  Purple = 'purple',
  Orange = 'orange',
  Pink = 'pink',
  Cyan = 'cyan',
  Gray = 'gray',
  Silver = 'silver'
}

export interface Board {
  _id: string;
  name: string;
  description?: string;
  types?: BoardType[];
  customFields?: any[];
  groups?: any[];
}

export interface BoardsResponse {
  type: string;
  payload: {
    boards: Board[];
  };
}

export interface BoardResponse {
  type: string;
  payload: {
    board: Board;
  };
}

// Profile interfaces
export interface Profile {
  _id: string;
  name: string;
  email: string;
  avatar?: string;
  role?: string;
}

export interface ProfileResponse {
  type: string;
  payload: {
    profile: Profile;
  };
}

// Milestone interfaces
export interface Milestone {
  _id: string;
  name: string;
  description?: string;
  dueDate?: Date;
  completed?: boolean;
  tasks?: string[];
  createdAt?: Date;
  updatedAt?: Date;
}

export interface MilestonesResponse {
  type: string;
  payload: {
    milestones: Milestone[];
  };
}

export interface CreateMilestoneRequest {
  name: string;
  description?: string;
  dueDate?: Date;
  members?: string[];
}

export interface CreateMilestoneResponse {
  type: string;
  payload: {
    milestone: Milestone;
  };
}

export interface GetMilestoneResponse {
  type: string;
  payload: {
    milestone: Milestone;
  };
}

export interface EditMilestoneRequest {
  _id: string;
  name?: string;
  description?: string;
  dueDate?: Date;
  members?: string[];
}

export interface EditMilestoneResponse {
  type: string;
  payload: {
    milestone: Milestone;
  };
}

export interface ToggleMilestoneRequest {
  task: string;
  milestones: string[];
}

export interface ToggleMilestoneResponse {
  type: string;
  payload: {
    task: Task;
  };
}

// Upload interfaces
export interface UploadedFile {
  id: string;
  url: string;
  name: string;
  ext: string;
  type: EUploadFileType;
  dimension?: string;
  size: number;
  mime: string;
}

export interface UploadFileResponse {
  type: string;
  file: UploadedFile;
}

// Comment interfaces
export interface CommentReaction {
  id: string;
  name: string;
  native: string;
  unified: string;
  keywords: string[];
  shortcodes: string;
  user: string;
}

export interface Comment {
  id: string;
  content: string;
  author: {
    id: string;
    name: string;
    avatar?: string;
  };
  documentId: string;
  replyTo?: string;
  files: TaskFile[];
  reactions: CommentReaction[];
  createdAt: Date;
  editedAt?: Date;
  deletedAt?: Date;
}

export interface PostCommentRequest {
  document_id: string;
  content: string;
  file_ids?: string[];
  reply_to?: string;
}

export interface PostCommentResponse {
  type: string;
  comment: Comment;
}

export interface ReactToCommentRequest {
  comment_id: string;
  id: string;
  name: string;
  native: string;
  unified: string;
  keywords?: string[];
  shortcodes?: string;
}

export interface ReactToCommentResponse {
  type: string;
  reaction: CommentReaction;
}

export interface GetCommentsRequest {
  document_id: string;
}

export interface GetCommentsResponse {
  type: string;
  comments: Comment[];
}

export interface EditCommentRequest {
  content: string;
  comment_id: string;
  add_file_ids?: string[];
  order_file_ids?: string[];
  remove_file_ids?: string[];
}

export interface EditCommentResponse {
  type: string;
  comment: Comment;
}

export interface DeleteCommentRequest {
  comment_id: string;
}

export interface DeleteCommentResponse {
  type: string;
  comment: Comment;
}

// Board creation/editing interfaces
export interface CreateBoardTypeRequest {
  boardId: string;
  label: string;
  icon: string;
  color: string;
}

export interface CreateBoardTypeResponse {
  type: string;
  board_type: BoardType;
}

export interface EditBoardTypeRequest {
  id: string;
  label?: string;
  icon?: string;
  color?: string;
}

export interface EditBoardTypeResponse {
  type: string;
  board_type: BoardType;
}

export interface CreateBoardCustomFieldRequest {
  boardId: string;
  name: string;
  type: CustomFieldType;
  options?: string[];
}

export interface CreateBoardCustomFieldResponse {
  type: string;
  customField: CustomField;
}

export interface EditBoardCustomFieldRequest {
  id: string;
  name?: string;
  type?: CustomFieldType;
  options?: string[];
}

export interface EditBoardCustomFieldResponse {
  type: string;
  customField: CustomField;
}

export interface CreateBoardGroupRequest {
  boardId: string;
  name: string;
  color?: string;
}

export interface CreateBoardGroupResponse {
  type: string;
  group: {
    id: string;
    name: string;
    color?: string;
  };
}

export interface EditBoardGroupRequest {
  id: string;
  name?: string;
  color?: string;
}

export interface EditBoardGroupResponse {
  type: string;
  group: {
    id: string;
    name: string;
    color?: string;
  };
}

// Comment reaction metadata
export const COMMENT_REACTION_METADATA: Record<CommentReactionType, {
  id: string;
  name: string;
  native: string;
  unified: string;
  keywords: string[];
  shortcodes: string;
}> = {
  [CommentReactionType.ThumbsUp]: {
    id: 'thumbsup',
    name: 'Thumbs Up',
    native: '👍',
    unified: '1f44d',
    keywords: ['thumbs', 'up', 'like', 'approve', 'good'],
    shortcodes: ':thumbsup:'
  },
  [CommentReactionType.ThumbsDown]: {
    id: 'thumbsdown',
    name: 'Thumbs Down',
    native: '👎',
    unified: '1f44e',
    keywords: ['thumbs', 'down', 'dislike', 'disapprove', 'bad'],
    shortcodes: ':thumbsdown:'
  },
  [CommentReactionType.Heart]: {
    id: 'heart',
    name: 'Red Heart',
    native: '❤️',
    unified: '2764-fe0f',
    keywords: ['love', 'heart', 'like', 'emotion'],
    shortcodes: ':heart:'
  },
  [CommentReactionType.Laugh]: {
    id: 'laugh',
    name: 'Face with Tears of Joy',
    native: '😂',
    unified: '1f602',
    keywords: ['laugh', 'funny', 'lol', 'joy'],
    shortcodes: ':joy:'
  },
  [CommentReactionType.Surprised]: {
    id: 'surprised',
    name: 'Face with Open Mouth',
    native: '😮',
    unified: '1f62e',
    keywords: ['surprised', 'wow', 'amazed', 'shock'],
    shortcodes: ':open_mouth:'
  },
  [CommentReactionType.Sad]: {
    id: 'sad',
    name: 'Crying Face',
    native: '😢',
    unified: '1f622',
    keywords: ['sad', 'cry', 'tear', 'emotion'],
    shortcodes: ':cry:'
  },
  [CommentReactionType.Angry]: {
    id: 'angry',
    name: 'Pouting Face',
    native: '😡',
    unified: '1f621',
    keywords: ['angry', 'mad', 'annoyed', 'emotion'],
    shortcodes: ':rage:'
  }
};