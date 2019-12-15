import axios from 'axios'
import Cookie from 'js-cookie'


const http = axios.create({
  timeout: 5000,
  baseURL: "http://127.0.0.1:9998/",
  responseType: 'json',
});


http.interceptors.request.use(
  config => {
    let token = Cookie.get("token");
    if (token) {
      config.headers['Authorization'] = token;
    }
    // config.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8';
    // console.log('请求', config);
    return config;
  },
  error => {
    console.log("请求报错", error)
    return Promise.reject(error);
  });


http.interceptors.response.use(
  response => {
    return response
  }, error => {
    console.log(error)
    if (error.response.status === 403) {
      if ("您没有执行该操作的权限。" == error.response.data.detail) {
        window.location.href = "/403/"
      } else {
        window.location.href = "/login/"
      }
    }
    return Promise.reject(error.response);
  }
);

export default http;