"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.BoardsAPI = exports.BoardsResponseSchema = exports.BoardSchema = void 0;
const BaseAPIClient_1 = require("../client/BaseAPIClient");
const zod_1 = require("zod");
exports.BoardSchema = zod_1.z.object({
    _id: zod_1.z.string(),
    name: zod_1.z.string(),
});
exports.BoardsResponseSchema = zod_1.z.object({
    boards: zod_1.z.array(exports.BoardSchema),
});
class BoardsAPI extends BaseAPIClient_1.BaseAPIClient {
    getBoards() {
        return __awaiter(this, void 0, void 0, function* () {
            const res = yield this.http.get('/boards');
            return exports.BoardsResponseSchema.parse(res.data);
        });
    }
}
exports.BoardsAPI = BoardsAPI;
