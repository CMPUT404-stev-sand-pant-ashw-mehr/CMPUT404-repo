import axios from "axios";

import {
  GET_POSTS,
  DELETE_POST,
  CREATE_POST,
  GET_ALERTS,
  CREATE_ALERT,
} from "./types";

import { tokenConfig } from "./auth";

export const getPosts = () => (dispatch, getState) => {
  axios
    .get(`/backend/posts`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: GET_POSTS,
        payload: res.data,
      });
    })
    .catch((err) => {
      const alert = {
        msg: err.response.data,
        status: err.response.status,
      };
      dispatch({
        type: GET_ALERTS,
        payload: alert,
      });
    });
};

export const deletePost = (id) => (dispatch, getState) => {
  axios
    .delete(`/backend/posts/${id}`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { success: "Post has been deleted!" },
          status: res.status,
        },
      });
      dispatch({
        type: DELETE_POST,
        payload: id,
      });
    })
    .catch((err) => {
      const alert = {
        msg: err.response.data,
        status: err.response.status,
      };
      dispatch({
        type: GET_ALERTS,
        payload: alert,
      });
    });
};

export const createPost = (post) => (dispatch, getState) => {
  axios
    .post(`/backend/posts/`, post, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { success: "Post has been created!" },
          status: res.status,
        },
      });
      dispatch({
        type: CREATE_POST,
        payload: res.data,
      });
    })
    .catch((err) => {
      const alert = {
        msg: err.response.data,
        status: err.response.status,
      };
      dispatch({
        type: GET_ALERTS,
        payload: alert,
      });
    });
};
