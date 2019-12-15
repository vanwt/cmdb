from .models import Menu


def jwt_response(token, user=None, request=None):
    if user.is_superuser:
        menus = Menu.objects.all()
        user_menu = []
        for menu in menus:
            if menu.is_parent:
                c = {
                    "name": menu.name,
                    "icon": menu.icon,
                    "label": menu.title,
                    "url": menu.url,
                    "path": menu.path,
                }
                # 父组件
                for m in menu.childrens.all():
                    c.setdefault("children", []).append({
                        "name": m.name,
                        "icon": m.icon,
                        "label": m.title,
                        "url": m.url,
                        "path": m.path,
                    })
                user_menu.append(c)
    else:
        menus = Menu.objects.none()
        for role in user.roles.all():
            menus |= role.menu.all()

        user_menu = []
        for menu in menus:
            if menu.is_parent:
                c = {
                    "name": menu.name,
                    "icon": menu.icon,
                    "label": menu.title,
                    "url": menu.url,
                    "path": menu.path,
                }
                # 父组件
                for m in menu.childrens.all():
                    if c.get("children", None) is None:
                        c["children"] = []
                    if m in menus:
                        c["children"].append({
                            "name": m.name,
                            "icon": m.icon,
                            "label": m.title,
                            "url": m.url,
                            "path": m.path,
                        })
                user_menu.append(c)

    content = {
        "code": 0,
        "msg": "Success !",
        "token": token,
        "username": user.username,
        "realname": user.realname if user.realname else user.username,
        "lastlogin": user.last_login,
        "menu": user_menu
    }
    return content
