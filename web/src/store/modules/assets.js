export default {
  state: {
    // 页面切换
    assetsList: [],
  },
  getters: {
    getAssetsId(state) {
      return state.assetsList
    }
  },
  mutations: {
    setAssetsId(state, asset) {
      // 需要判断添加的tab有没有在里
      let result = state.assetsList.findIndex(item => item.path === asset.path);
      result === -1 ? state.assetsList.push(asset) : ""
    },

  }
}