import Cookie from 'js-cookie'

export default {
  state: {
    // 左侧导航 具体是登陆后存到cookie 然后每次去cookie中读取
    menu: [
    ],
    menu2: [
      {
        path: "/home",
        url: 'home/home',
        label: "首页",
        name: "home",
        icon: "s-home"
      },
      {
        label: "资产管理",
        icon: "cpu",
        children: [
          {
            path: "/server",
            url: "assets/server",
            name: "server",
            label: "物理机",
            icon: "s-platform"
          },
          {
            path: "/vm",
            url: "assets/vm",
            name: "vm",
            label: "虚拟机",
            icon: "s-platform"
          },
          {
            path: "/all_server",
            url: "assets/all_server",
            name: "all_server",
            label: "全部主机",
            icon: "s-platform"
          }
        ]
      },
      {
        label: "用户管理",
        icon: "user",
        children: [
          {
            path: "/users",
            url: "user/users",
            name: "user",
            label: "全部用户",
            icon: "s-custom"
          },
          {
            path: "/permission",
            url: "user/permission",
            name: "permission",
            label: "权限管理",
            icon: "lock"
          },
          {
            path: "/menu",
            url: "user/menu",
            name: "menu",
            label: "菜单管理",
            icon: "menu"
          },
          {
            path: "/role",
            url: "user/role",
            name: "role",
            label: "角色管理",
            icon: "user-solid"
          }
        ]
      },
    ],
    // 导航栏的展示与隐藏 true 为隐藏
    isCollapse: true,
    // 页面切换
  },
  getters: {
    getMenu(state) {
      return state.menu
    },
    getCollapse(state) {
      return state.isCollapse
    }
  },
  mutations: {
    setMenu(state, val) {
      state.menu = val;
      Cookie.set('menu', JSON.stringify(val))
    },
    clearMenu(state) {
      state.Menu = [];
      Cookie.remove('menu')
    },
    MenuToRouter(state, router) {
      if (state.menu.length === 0) {
        let menu = Cookie.get('menu');
        if (!menu) {
          return
        }
        state.menu = JSON.parse(menu);
      }
      // 循环拼接所有url
      let currentMenu = [
        {
          path: '/',
          component: () => import('@/views/Main'),
          children: []
        }
      ];
      // 拼接url
      state.menu.forEach(item => {
        if (item.children) {
          // 有子路由
          item.children = item.children.map(item => {
            item.component = () => import(`@/views/${item.url}`);
            return item
          });
          currentMenu[0].children.push(...item.children)
        } else {
          // 没有子路由
          item.component = () => import(`@/views/${item.url}`);
          currentMenu[0].children.push(item)
        }
      });
      // console.log('cur', currentMenu);
      router.addRoutes(currentMenu)
    },
    setCollapse(state) {
      state.isCollapse = !state.isCollapse
    },

  },
  actions: {
    setItem(content, item) {
      // item.name === 'home' ? content.commit("setMenuItem",null) :  content.commit("setMenuItem",item)
      if (item.name !== 'home') {
        // 不是home 让header的部分显示当前路由
        content.commit("setHeaderMenu", item);
        // 添加到视图栏
        content.commit("setTab", item)
      } else {
        content.commit("setHeaderMenu", undefined);
      }
    }
  },
}