import axios from "axios";

import {
  GET_ALERTS,
  GET_GITHUB,
} from "./types";

import { tokenConfig } from "./auth";

export const getGithub = (github) => dispatch => {
    axios
        .get(`https://api.github.com/users/${github}/events/public` )
        .then(res => {
            dispatch({
                type: GET_GITHUB,
                payload: res.data
            });
        }).catch(err => {
            const alert = {
                msg: err.response.data,
                origin: GET_GITHUB,
                status: err.response.status
            }
            dispatch({
                type: GET_ALERTS,
                payload: alert,
            })
        });
}
