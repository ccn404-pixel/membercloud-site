import { json, configured } from '../lib/shared.js';
export const onRequestGet = ({ env }) => json(configured(env));
