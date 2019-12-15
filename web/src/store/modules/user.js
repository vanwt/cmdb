import Cookie from 'js-cookie'
import da from "element-ui/src/locale/lang/da";

export default {
  state: {
    token: "",
    realname: "",
    username: "",
    lastlogin: "",
  },
  getters: {
    getToken(state) {
      return state.token
    },
    getUser(state) {
      return {
        realname: state.realname,
        username: state.username,
        lastlogin: state.lastlogin,
      }
    }
  },
  mutations: {
    setToken(state, val) {
      state.token = val;
      Cookie.set('token', val)
    },
    clearToken(state) {
      state.token = "";
      Cookie.remove("token")
    },
    clearUser(state) {
      Cookie.remove('realname');
      Cookie.remove('username');
      Cookie.remove('lastlogin');
      state.username = "";
      state.realname = "";
      state.lastlogin = "";
    },
    getToken(state) {
      let token = Cookie.get("token");
      if (!token) {
        return
      }
      state.token = token
    },
    getUser(state) {
      let username = Cookie.get('username');
      let realname = Cookie.get('realname');
      let lastlogin = Cookie.get('lastlogin');
      if (!username || !realname) {
        return
      }
      state.username = username;
      state.realname = realname;
      state.lastlogin = lastlogin
    },
    setUser(state, data) {
      Cookie.set('username', data.username);
      Cookie.set('realname', data.realname);
      Cookie.set('lastlogin', data.lastlogin);
      state.username = data.username;
      state.realname = data.realname;
      state.lastlogin = data.lastlogin
    }
  }
}