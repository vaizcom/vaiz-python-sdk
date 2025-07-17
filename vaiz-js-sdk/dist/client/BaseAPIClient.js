"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.BaseAPIClient = void 0;
const axios_1 = __importDefault(require("axios"));
class BaseAPIClient {
    constructor(config) {
        this.config = config;
        this.http = axios_1.default.create({
            baseURL: config.baseUrl || 'https://api.vaiz.app/v4',
            timeout: config.timeout || 10000,
        });
        this.http.interceptors.request.use((req) => {
            req.headers = req.headers || {};
            req.headers['Authorization'] = `Bearer ${this.config.apiKey}`;
            req.headers['X-Space-Id'] = this.config.spaceId;
            return req;
        });
    }
}
exports.BaseAPIClient = BaseAPIClient;
