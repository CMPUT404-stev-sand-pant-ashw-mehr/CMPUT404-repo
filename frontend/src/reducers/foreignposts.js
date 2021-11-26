import { GET_FOREIGN_POSTS } from "../actions/types.js";

const initialState = {
  posts: [],
};

export default function (state = initialState, action) {
  switch (action.type) {
    case GET_FOREIGN_POSTS:
      return {
        ...state,
        posts: action.payload.items,
      };
    default:
      return state;
  }
}
