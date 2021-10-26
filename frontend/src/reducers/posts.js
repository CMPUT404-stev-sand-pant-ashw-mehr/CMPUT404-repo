import { GET_POSTS, DELETE_POST, CREATE_POST } from "../actions/types.js";

const initialState = {
  posts: [],
  count: "",
  next: "",
  previous: "",
  page: 1,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case GET_POSTS:
      return {
        ...state,
        posts: action.payload.results,
        count: action.payload.count,
        next: action.payload.next,
        previous: action.payload.previous,
        page: action.page,
      };
    case CREATE_POST:
      return {
        ...state,
        posts: [...state.posts, action.payload],
        count: (state.count += 1),
      };
    case DELETE_POST:
      return {
        ...state,
        posts: state.posts.filter((post) => post.id !== action.payload),
        count: (state.count -= 1),
      };
    default:
      return state;
  }
}
