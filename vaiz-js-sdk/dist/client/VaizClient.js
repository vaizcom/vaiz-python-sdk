"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.VaizClient = void 0;
const BaseAPIClient_1 = require("./BaseAPIClient");
const boards_1 = require("../api/boards");
class VaizClient extends BaseAPIClient_1.BaseAPIClient {
    constructor(config) {
        super(config);
        this.boards = new boards_1.BoardsAPI(config);
    }
}
exports.VaizClient = VaizClient;
