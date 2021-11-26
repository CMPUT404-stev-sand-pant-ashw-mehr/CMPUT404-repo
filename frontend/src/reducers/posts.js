import {
  GET_POSTS,
  DELETE_POST,
  CREATE_POST,
  CREATE_POST_COMMENT,
  UPDATE_POST,
  LIKE_POST,
} from "../actions/types.js";

const initialState = {
  posts: [],
  next: "",
  previous: "",
  page: 1,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case GET_POSTS:
      return {
        ...state,
        posts: action.payload.items,
        next: action.payload.next,
        previous: action.payload.previous,
        page: action.page,
      };
    case CREATE_POST_COMMENT:
    case CREATE_POST:
      return {
        ...state,
        posts: [...state.posts, action.payload],
      };
    case DELETE_POST:
      return {
        ...state,
        posts: state.posts.filter((post) => post.id !== action.payload),
      };
    case LIKE_POST:
      return {
        ...state,
        posts: [...state.posts, action.payload],
      };
    default:
      return state;
  }
}
