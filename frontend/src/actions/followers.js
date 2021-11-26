import axios from "axios";

import {
  GET_FOLLOWERS,
  DELETE_FOLLOWER,
  ADD_FOLLOWER,
  CHECK_FOLLOWER,
} from "./types";

import { tokenConfig } from "./auth";

export const getFollowers = (dispatch, getState) => {
  const authorId = getState().auth.user.author;
  axios
    .get(`/author/${authorId}/followers`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: GET_FOLLOWERS,
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

export const deleteFollower = (foreignAuthorId) => (dispatch, getState) => {
  const authorId = getState().auth.user.author;

  axios
    .delete(
      `/author/${authorId}/followers/${foreignAuthorId}`,
      tokenConfig(getState)
    )
    .then((res) => {
      dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { success: "You have unfollowed that author!" },
          status: res.status,
        },
      });
      dispatch({
        type: DELETE_FOLLOWER,
        payload: foreignAuthorId,
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

export const addFollower = (foreignAuthorId) => (dispatch, getState) => {
  const authorId = getState().auth.user.author;
  axios
    .put(
      `/author/${authorId}/followers/${foreignAuthorId}`,
      tokenConfig(getState)
    )
    .then((res) => {
      dispatch({
        type: CREATE_ALERT,
        payload: {
          msg: { success: "You have followed that user!" },
          status: res.status,
        },
      });
      dispatch({
        type: ADD_FOLLOWER,
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

export const checkFollower = (foreignAuthorId) => (dispatch, getState) => {
  const authorId = getState().auth.user.author;
  axios
    .get(
      `/author/${authorId}/followers/${foreignAuthorId}`,
      tokenConfig(getState)
    ).then((res) => {
      console.log("response - ", res);
      dispatch({
        type: CHECK_FOLLOWER,
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
