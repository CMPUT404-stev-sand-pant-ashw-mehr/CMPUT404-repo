import { GET_FOREIGN_POSTS, LIKE_FOREIGN_POST } from "../actions/types.js";

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
    case LIKE_FOREIGN_POST:
      let newPosts = state.posts;
      let replacePost = state.posts.find(
        (post) => post.id === action.payload.id
      );
      Object.assign(replacePost, action.payload);

      return {
        ...state,
        posts: newPosts,
      };
    default:
      return state;
  }
}
