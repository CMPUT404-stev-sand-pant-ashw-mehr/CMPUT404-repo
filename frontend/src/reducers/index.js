import { combineReducers } from "redux";
import posts from "./posts";
import foreignposts from "./foreignposts";
import post from "./post";
import alerts from "./alerts";
import auth from "./auth";

export default combineReducers({
  posts,
  post,
  foreignposts,
  alerts,
  auth,
});
