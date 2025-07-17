import { BaseAPIClient } from './base';
import {
  PostCommentRequest,
  PostCommentResponse,
  ReactToCommentRequest,
  ReactToCommentResponse,
  GetCommentsRequest,
  GetCommentsResponse,
  EditCommentRequest,
  EditCommentResponse,
  DeleteCommentRequest,
  DeleteCommentResponse,
  CommentReactionType,
  COMMENT_REACTION_METADATA,
} from './types';

export class CommentsAPIClient extends BaseAPIClient {
  
  async postComment(
    documentId: string,
    content: string,
    fileIds?: string[],
    replyTo?: string
  ): Promise<PostCommentResponse> {
    /**
     * Post a comment to a document.
     * 
     * @param documentId The ID of the document to comment on
     * @param content The comment content (can include HTML)
     * @param fileIds List of file IDs to attach to the comment
     * @param replyTo ID of the comment to reply to (for threaded replies)
     * 
     * @returns The created comment information
     */
    const request: PostCommentRequest = {
      document_id: documentId,
      content,
      file_ids: fileIds || [],
      reply_to: replyTo
    };
    
    const responseData = await this.request<PostCommentResponse>('postComment', 'POST', request);
    return responseData;
  }
  
  async reactToComment(
    commentId: string,
    emojiId: string,
    emojiName: string,
    emojiNative: string,
    emojiUnified: string,
    emojiKeywords?: string[],
    emojiShortcodes?: string
  ): Promise<ReactToCommentResponse> {
    /**
     * Add a reaction to a comment.
     * 
     * @param commentId The ID of the comment to react to
     * @param emojiId The emoji ID (e.g., "kissing_smiling_eyes")
     * @param emojiName The human-readable emoji name (e.g., "Kissing Face with Smiling Eyes")
     * @param emojiNative The emoji character (e.g., "😙")
     * @param emojiUnified The Unicode codepoint (e.g., "1f619")
     * @param emojiKeywords Keywords for the emoji
     * @param emojiShortcodes Shortcode for the emoji (e.g., ":kissing_smiling_eyes:")
     * 
     * @returns The reaction information
     */
    const request: ReactToCommentRequest = {
      comment_id: commentId,
      id: emojiId,
      name: emojiName,
      native: emojiNative,
      unified: emojiUnified,
      keywords: emojiKeywords || [],
      shortcodes: emojiShortcodes || `:${emojiId}:`
    };
    
    const responseData = await this.request<ReactToCommentResponse>('reactToComment', 'POST', request);
    return responseData;
  }
  
  async addReaction(
    commentId: string,
    reaction: CommentReactionType
  ): Promise<ReactToCommentResponse> {
    /**
     * Add a popular emoji reaction to a comment (simplified API).
     * 
     * @param commentId The ID of the comment to react to
     * @param reaction The type of reaction to add
     * 
     * @returns The reaction information
     */
    const metadata = COMMENT_REACTION_METADATA[reaction];
    
    return this.reactToComment(
      commentId,
      metadata.id,
      metadata.name,
      metadata.native,
      metadata.unified,
      metadata.keywords,
      metadata.shortcodes
    );
  }
  
  async getComments(documentId: string): Promise<GetCommentsResponse> {
    /**
     * Get all comments for a document.
     * 
     * @param documentId The ID of the document to get comments for
     * 
     * @returns The list of comments for the document
     */
    const request: GetCommentsRequest = {
      document_id: documentId
    };
    
    const responseData = await this.request<GetCommentsResponse>('getComments', 'POST', request);
    return responseData;
  }
  
  async editComment(
    commentId: string,
    content: string,
    addFileIds?: string[],
    orderFileIds?: string[],
    removeFileIds?: string[]
  ): Promise<EditCommentResponse> {
    /**
     * Edit an existing comment.
     * 
     * @param commentId The ID of the comment to edit
     * @param content The new content for the comment (HTML supported)
     * @param addFileIds File IDs to add to the comment
     * @param orderFileIds File IDs in new order
     * @param removeFileIds File IDs to remove from the comment
     * 
     * @returns The updated comment
     */
    const request: EditCommentRequest = {
      content,
      comment_id: commentId,
      add_file_ids: addFileIds || [],
      order_file_ids: orderFileIds || [],
      remove_file_ids: removeFileIds || []
    };
    
    const responseData = await this.request<EditCommentResponse>('editComment', 'POST', request);
    return responseData;
  }
  
  async deleteComment(commentId: string): Promise<DeleteCommentResponse> {
    /**
     * Delete a comment (soft delete).
     * 
     * @param commentId The ID of the comment to delete
     * 
     * @returns The deleted comment with deleted_at timestamp
     */
    const request: DeleteCommentRequest = {
      comment_id: commentId
    };
    
    const responseData = await this.request<DeleteCommentResponse>('deleteComment', 'POST', request);
    return responseData;
  }
}