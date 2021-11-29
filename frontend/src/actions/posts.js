import axios from "axios";

import {
  GET_POSTS,
  GET_AUTHOR_POSTS,
  GET_FOREIGN_POSTS,
  GET_POST,
  DELETE_POST,
  CREATE_POST,
  GET_ALERTS,
  CREATE_ALERT,
  CREATE_POST_COMMENT,
  LIKE_POST,
  LIKE_POST_COMMENT,
} from "./types";

import { tokenConfig } from "./auth";

export const getPosts =
  (page = 1) =>
  (dispatch, getState) => {
    axios
      .get(`/posts?page=${page}`, tokenConfig(getState))
      .then((res) => {
        dispatch({
          type: GET_POSTS,
          payload: res.data,
          page: page,
        });
      })
      .catch((err) => {
        const alert = {
          msg: err.response,
          status: err.response,
        };
        dispatch({
          type: GET_ALERTS,
          payload: alert,
        });
      });
  };

export const getAuthorPosts =
  (authorId = getState().auth.user.author, page = 1) =>
  (dispatch, getState) => {
    axios
      .get(`/author/${authorId}/posts?page=${page}`, tokenConfig(getState))
      .then((res) => {
        dispatch({
          type: GET_AUTHOR_POSTS,
          payload: res.data,
          page: page,
        });
      })
      .catch((err) => {
        const alert = {
          msg: err.response,
          status: err.response,
        };
        dispatch({
          type: GET_ALERTS,
          payload: alert,
        });
      });
  };

export const getForeignPosts = () => (dispatch, getState) => {
  axios
    .get(`/connection/posts`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: GET_FOREIGN_POSTS,
        payload: res.data,
      });
    })
    .catch((err) => {
      const alert = {
        msg: err.response,
        status: err.response,
      };
      dispatch({
        type: GET_ALERTS,
        payload: alert,
      });
    });
};

export const getPost = (authorId, postId) => (dispatch, getState) => {
  axios
    .get(`/author/${authorId}/posts/${postId}`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: GET_POST,
        payload: res.data,
      });
    })
    .catch((err) => {
      const alert = {
        msg: err.response,
        status: err.response,
      };
      dispatch({
        type: GET_ALERTS,
        payload: alert,
      });
    });
};

export const deletePost = (id) => (dispatch, getState) => {
  const authorId = getState().auth.user.author;
  const urlId = id.split("/").pop();
  axios
    .delete(`/author/${authorId}/posts/${urlId}`, tokenConfig(getState))
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
  const authorId = getState().auth.user.author;
  axios
    .post(`/author/${authorId}/posts/`, post, tokenConfig(getState))
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

export const createPostComment = (postId, comment) => (dispatch, getState) => {
  const authorId = getState().auth.user.author;
  axios
    .post(
      `/author/${authorId}/posts/${postId}/comments`,
      comment,
      tokenConfig(getState)
    )
    .then((res) => {
      dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { success: "Comment has been added!" },
          status: res.status,
        },
      });
      dispatch({
        type: CREATE_POST_COMMENT,
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

export const likePost = (authorId, postId) => (dispatch, getState) => {
  const authorId = getState().auth.user.author;

  axios
    .post(
      `/author/${authorId}/post/${postId}/likes`,
      null,
      tokenConfig(getState)
    )
    .then((res) => {
      dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { success: `${likeType} has been liked!` },
          status: res.status,
        },
      });
      dispatch({
        type: LIKE_POST,
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

export const likeObject = (likeObject, likeType) => (dispatch, getState) => {
  const authorId = getState().auth.user.author;

  axios
    .post(`/author/${authorId}/inbox/`, likeObject, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { success: `${likeType} has been liked!` },
          status: res.status,
        },
      });
      dispatch({
        type: LIKE_OBJECT,
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
