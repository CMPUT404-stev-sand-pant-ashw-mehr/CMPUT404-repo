import { combineReducers } from "redux";
import posts from "./posts";
import authorposts from "./authorposts";
import foreignposts from "./foreignposts";
import post from "./post";
import followers from "./followers";
import alerts from "./alerts";
import auth from "./auth";

export default combineReducers({
  posts,
  post,
  authorposts,
  foreignposts,
  alerts,
  followers,
  auth,
});
