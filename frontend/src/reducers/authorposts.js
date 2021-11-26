import { GET_AUTHOR_POSTS } from "../actions/types.js";

const initialState = {
  posts: [],
  count: "",
  next: "",
  previous: "",
  page: 1,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case GET_AUTHOR_POSTS:
      return {
        ...state,
        posts: action.payload.items,
        count: action.payload.count,
        next: action.payload.next,
        previous: action.payload.previous,
        page: action.page,
      };
    default:
      return state;
  }
}
