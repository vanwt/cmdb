
import Cookie from 'js-cookie'

export default {
  state: {
    // 页面切换
    tabsList: [{
      name: "home",
      path: "/",
      label: "首页"
    }],
    menuItem: undefined,
  },
  getters: {
    getTabs(state) {
      return state.tabsList
    },
    getMenuItem(state) {
      return state.menuItem
    },
  },
  mutations: {
    setTab(state, tab) {
      // 需要判断添加的tab有没有在里
      let result = state.tabsList.findIndex(item => item.name === tab.name);
      result === -1 ? state.tabsList.push(tab) : ""
    },
    closeTab(state, val) {
      let result = state.tabsList.findIndex(item => item.name === val.name);
      state.tabsList.splice(result, 1)
      // 删除之后还要跳转到上一个的页面
    },
    setHeaderMenu(state, item) {
      state.menuItem = item
    }
  }
}