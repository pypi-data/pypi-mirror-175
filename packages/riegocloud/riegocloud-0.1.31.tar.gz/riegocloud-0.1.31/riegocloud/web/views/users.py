import aiohttp_jinja2
from aiohttp import web

from logging import getLogger
_log = getLogger(__name__)


class Users():
    def __init__(self, app, db, security):
        self._db = db
        self._security = security
        app.router.add_get('/users', self._index, name='users')
        app.router.add_get('/users/new', self._new, name='users_new')
        app.router.add_post('/users/new', self._new_apply)
        app.router.add_get('/users/{item_id}',
                           self._view, name='users_view')
        app.router.add_get('/users/{item_id}/edit',
                           self._edit, name='users_edit')
        app.router.add_post('/users/{item_id}/edit', self._edit_apply)
        app.router.add_get('/users/{item_id}/delete',
                           self._delete, name='users_delete')

    @ aiohttp_jinja2.template("users/index.html")
    async def _index(self, request: web.Request):
        await self._security.raise_perm(request, perm='superuser')
        cursor = await self._db.conn.cursor()
        await cursor.execute('SELECT * FROM users')
        items = await cursor.fetchall()
        await cursor.close()
        return {"items": items}

    @ aiohttp_jinja2.template("users/new.html")
    async def _new(self, request: web.Request):
        await self._security.raise_perm(request, perm='superuser')
        return {}

    async def _new_apply(self, request: web.Request):
        await self._security.raise_perm(request, perm='superuser')
        item = await request.post()
        cursor = await self._db.conn.cursor()
        try:
            await cursor.execute(
                ''' INSERT INTO users
                    (identity, password,
                    full_name, email,
                    permission_id, is_superuser,
                    is_disabled, remember_me)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ''',
                (item['identity'], item['password'],
                 item['full_name'], item['email'],
                 item['permission_id'], item['is_superuser'],
                 item['is_disabled'], item['remember_me']))
            await self._db.conn.commit()
        except Exception as e:
            await self._db.conn.rollback()
            _log.debug(f'users add: {e}')
            await cursor.close()
            return web.HTTPSeeOther(request.app.router['users_new'].url_for())
        item_id = str(cursor.lastrowid)
        await cursor.close()
        return web.HTTPSeeOther(
            request.app.router['users_view'].url_for(item_id=item_id))

    @ aiohttp_jinja2.template("users/view.html")
    async def _view(self, request: web.Request):
        await self._security.raise_perm(request, perm='superuser')
        item_id = request.match_info["item_id"]
        cursor = await self._db.conn.cursor()
        await cursor.execute('SELECT * FROM users WHERE id=%s', (item_id,))
        item = await cursor.fetchone()
        await cursor.close()
        if item is None:
            return web.HTTPSeeOther(request.app.router['users'].url_for())
        return {"item": item}

    @ aiohttp_jinja2.template("users/edit.html")
    async def _edit(self, request: web.Request):
        await self._security.raise_perm(request, perm='superuser')
        item_id = request.match_info["item_id"]
        cursor = await self._db.conn.cursor()
        await cursor.execute('SELECT * FROM users WHERE id=%s', (item_id,))
        item = await cursor.fetchone()
        await cursor.close()
        if item is None:
            return web.HTTPSeeOther(request.app.router['users'].url_for())
        return {"item": item}

    async def _edit_apply(self, request: web.Request):
        await self._security.raise_perm(request, perm='superuser')
        item_id = request.match_info["item_id"]
        item = await request.post()
        cursor = await self._db.conn.cursor()
        try:
            await cursor.execute(
                '''UPDATE users
                        SET identity = %s, password = %s,
                        full_name = %s, email = %s,
                        permission_id = %s, is_superuser = %s,
                        is_disabled = %s, remember_me = %s
                        WHERE id = %s ''',
                (item['identity'], item['password'],
                 item['full_name'], item['email'],
                 item['permission_id'], item['is_superuser'],
                 item['is_disabled'], item['remember_me'], item_id))
            await cursor.commit()
        except Exception as e:
            _log.debug(f'users: edit fail: {e}')
            return web.HTTPSeeOther(
                request.app.router['users_edit'].url_for(item_id=item_id))
        finally:
            rowcount = cursor.rowcount
            await cursor.close()
        if rowcount < 1:
            _log.debug('users: edit fail:')
            return web.HTTPSeeOther(
                request.app.router['users_edit'].url_for(item_id=item_id))
        return web.HTTPSeeOther(
            request.app.router['users_view'].url_for(item_id=item_id))

    async def _delete(self, request: web.Request):
        await self._security.raise_perm(request, perm='superuser')
        item_id = request.match_info["item_id"]
        if item_id is None or len(item_id) < 1:
            return web.HTTPSeeOther(request.app.router['users'].url_for())
        cursor = await self._db.conn.cursor()
        try:
            await cursor.execute(
                'DELETE FROM users WHERE id = %s',
                (item_id,))
            await self._db.conn.commit()
        except Exception as e:
            await self._db.conn.rollback()
            _log.debug(f'users delete fail: {e}')
            return web.HTTPSeeOther(
                request.app.router['users_delete'].url_for())
        finally:
            rowcount = cursor.rowcount
            await cursor.close()
        if rowcount < 1:
            _log.debug('users delete fail')
            return web.HTTPSeeOther(
                request.app.router['users_delete'].url_for())
        return web.HTTPSeeOther(request.app.router['users'].url_for())
