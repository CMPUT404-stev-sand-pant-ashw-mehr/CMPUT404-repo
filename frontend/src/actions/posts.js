import axios from "axios";

import { GET_POSTS, DELETE_POST, CREATE_POST } from "./types";

export const getPosts = () => (dispatch) => {
  axios
    .get(`/backend/posts`)
    .then((res) => {
      dispatch({
        type: GET_POSTS,
        payload: res.data,
      });
    })
    .catch((err) => console.log(err));
};

export const deletePost = (id) => (dispatch) => {
  axios
    .delete(`/backend/posts/${id}`)
    .then(() => {
      dispatch({
        type: DELETE_POST,
        payload: id,
      });
    })
    .catch((err) => console.log(err));
};

export const createPost = (post) => (dispatch) => {
  axios
    .post(`/backend/posts/`, post)
    .then((res) => {
      dispatch({
        type: CREATE_POST,
        payload: res.data,
      });
    })
    .catch((err) => console.log(err));
};
