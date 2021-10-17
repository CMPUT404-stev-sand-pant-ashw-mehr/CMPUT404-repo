import axios from "axios";

import {
  GET_POSTS,
  DELETE_POST,
  CREATE_POST,
  GET_ALERTS,
  CREATE_ALERT,
} from "./types";

export const getPosts = () => (dispatch) => {
  axios
    .get(`/backend/posts`)
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

export const deletePost = (id) => (dispatch) => {
  axios
    .delete(`/backend/posts/${id}`)
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

export const createPost = (post) => (dispatch) => {
  axios
    .post(`/backend/posts/`, post)
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
