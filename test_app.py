import os
from unittest import TestCase, main
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


EXECUTIVE_JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR2aU9BdnZLUDAtMDNrbk90U2xNSiJ9.eyJpc3MiOiJodHRwczovL2FwdGl2LXVzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjZiYWY5OTI1ZGQxNDAwNzhmZjkzZjEiLCJhdWQiOlsidGVzdCIsImh0dHBzOi8vYXB0aXYtdXMudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwMzgyODYxNywiZXhwIjoxNjA2NDIwNjE3LCJhenAiOiJQYmM2UGExMW96SXZpZ0NiWG5tWmZCNU90QWxhMGcweSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOmRyaW5rcyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6ZHJpbmtzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0OmRyaW5rcyIsInBvc3Q6bW92aWVzIl19.qzx3dsliw-Qt1ouGg9EXEe5DfjJ83d1c_7Z3vF5TaMzuRvmR17djEd5ppSb34aiuszYybzf4CyY9nbw1A1q0glPkkGfUp4pRMAjCep0Y2dZVtX-YGb2OQDARDiML5uU8pBni4CFv4Y84Fyc0BUmUZjbXIj-FHZ8xaB0P7l91JqayZe9fzml_uvPhu0ayFOi1wW4inIdL7oo7O3Alh2GrLsirMsExgIIidSJncuJevwpSUHUfGpvpXzX06s46ooPrGMCepvGFSA1KHFlXMfnP7medghI0hwbJM-s99vzTWh9UWYFn_vzWn8d_kb5CB3DjEDjTqownWYyVgHR0VC2GEQ"
DIRECTOR_JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR2aU9BdnZLUDAtMDNrbk90U2xNSiJ9.eyJpc3MiOiJodHRwczovL2FwdGl2LXVzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjcxMmM4NTgxNTUxZjAwNmU0MjFlZWIiLCJhdWQiOlsidGVzdCIsImh0dHBzOi8vYXB0aXYtdXMudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTYwMzkzODAyNywiZXhwIjoxNjA2NTMwMDI3LCJhenAiOiJQYmM2UGExMW96SXZpZ0NiWG5tWmZCNU90QWxhMGcweSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDpkcmlua3MtZGV0YWlsIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.WyZBYX-x8Fzdb8w2krWXVvPquZ2vwmaJDEwmvt7YgzsAce_TR4Q3Aug4xGAVxl5xGtcTppVhapSIR-XjwIjrX_UNPwIz9BsNcw2saMZ6j_pdLTrf3kPObVwCAcZRTDTGuwJbevaYtsPVAn2Y5NJeid2B5AP8rTdqmMG6NT8V3AbEP-v02IRSNatm51l1ybIESsGxdlxrhoeVEUoX8cm_lDzrumKWNLYfP9yhpM7nY1q7m2BgpdvWh1Yx30bxRw40svwcyJ6cflIO00nk4_Ft-CJIl6x6ynolMo6_DfNSlKkM93IO24E5iijbfPb10gsuhGeSX_qQYqFcc5tHsrxLBw"
ASSISTANT_JWT = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjR2aU9BdnZLUDAtMDNrbk90U2xNSiJ9.eyJpc3MiOiJodHRwczovL2FwdGl2LXVzLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDEwOTgyMjc5OTc5MjM4MTE4ODg2NSIsImF1ZCI6WyJ0ZXN0IiwiaHR0cHM6Ly9hcHRpdi11cy51cy5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjAzOTM3Nzg2LCJleHAiOjE2MDY1Mjk3ODYsImF6cCI6IlBiYzZQYTExb3pJdmlnQ2JYbm1aZkI1T3RBbGEwZzB5Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.l8YDZ-ZBsgwxKILaBdP7HQlysPBVBzwas5uNR_lTWt5SZ_kTjikxN-h-v-cjlnJDxn_jRIq09CoDlPGLt7aO3TXgheNCeq4hRG_c411CmS5xCgr8kNS49AxcT7UoOsRqREogrpcZPwZG2jCXRWNXJ8B7DNDDDb7VXIRwJVzzETThBPH7E4G_9FLOYprVqKXlHlajucHpqzqhwnMZlL-SnSZF8J9QIGLLAVuxCq5UEn2jW-U57tZ_RCx5uI6hh5BiV4hPMa3ratVYmJLE7VPuqzPacui-Ns99BDWOH91-41VGrL17zAhSM7p8iZxvJ_yJIoMHAhfMu6R6sFexbdYb1g"


class APITestCase(TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        database_name = "api_test.db"
        db_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_path = f"sqlite:///{os.path.join(db_dir, database_name)}"
        setup_db(self.app, self.database_path)

        self.new_movie = {"title": "Wonderful Life", "release_date": "2022-10-01"}
        self.new_actor = {"name": "Abby Bayer", "age": 49, "gender": "female"}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_post_actor_with_valid_auth(self):
        res = self.client().post(
            "/actors",
            json=self.new_actor,
            headers={"AUTHORIZATION": f"Bearer {DIRECTOR_JWT}"},
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_actor_with_no_permissio(self):
        res = self.client().post(
            "/actors",
            json=self.new_actor,
            headers={"AUTHORIZATION": f"Bearer {ASSISTANT_JWT}"},
        )

        self.assertEqual(res.status_code, 403)

    def test_get_actor_fail_if_no_auth(self):
        res = self.client().get("/actors",)

        self.assertEqual(res.status_code, 401)

    def test_get_actor_with_valid_auth(self):

        headers = {
            "Authorization": f"Bearer {ASSISTANT_JWT}",
        }

        res = self.client().get("/actors", headers=headers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_movie_with_no_permission(self):
        res = self.client().post(
            "/movies",
            json=self.new_movie,
            headers={"AUTHORIZATION": f"Bearer {DIRECTOR_JWT}"},
        )

        self.assertEqual(res.status_code, 403)

    def test_post_movie_with_valid_auth(self):
        res = self.client().post(
            "/movies",
            json=self.new_movie,
            headers={"AUTHORIZATION": f"Bearer {EXECUTIVE_JWT}"},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_movie_with_valid_auth(self):
        res = self.client().get(
            "/movies", headers={"AUTHORIZATION": f"Bearer {ASSISTANT_JWT}"}
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_get_movie_fail_if_no_auth(self):
        res = self.client().get("/movies")

        self.assertEqual(res.status_code, 401)

    def test_404_if_no_found_for_patch_actor(self):
        res = self.client().patch(
            "/actors/10",
            json={"age": 32},
            headers={"AUTHORIZATION": f"Bearer {EXECUTIVE_JWT}"},
        )
        self.assertEqual(res.status_code, 404)

    def test_404_if_no_found_for_delete_actor(self):
        res = self.client().delete(
            "/actors/10", headers={"AUTHORIZATION": f"Bearer {EXECUTIVE_JWT}"},
        )
        self.assertEqual(res.status_code, 404)

    def test_404_if_no_found_for_patch_movie(self):
        res = self.client().patch(
            "/movies/10",
            json={"title": "TBD"},
            headers={"AUTHORIZATION": f"Bearer {EXECUTIVE_JWT}"},
        )
        self.assertEqual(res.status_code, 404)

    def test_404_if_no_found_for_delete_movie(self):
        res = self.client().delete(
            "/movies/10", headers={"AUTHORIZATION": f"Bearer {EXECUTIVE_JWT}"},
        )
        self.assertEqual(res.status_code, 404)

    def test_patch_movie_with_valid_auth(self):
        res = self.client().patch(
            "/movies/2",
            json={"title": "TBD"},
            headers={"AUTHORIZATION": f"Bearer {EXECUTIVE_JWT}"},
        )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_patch_actor_with_valid_auth(self):
        res = self.client().patch(
            "/actors/2",
            json={"age": 32},
            headers={"AUTHORIZATION": f"Bearer {EXECUTIVE_JWT}"},
        )
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_with_valid_auth(self):
        res = self.client().delete(
            "/actors/1", headers={"AUTHORIZATION": f"Bearer {EXECUTIVE_JWT}"},
        )
        self.assertEqual(res.status_code, 200)

    def test_delete_movie_with_valid_auth(self):
        res = self.client().delete(
            "/movies/1", headers={"AUTHORIZATION": f"Bearer {EXECUTIVE_JWT}"},
        )
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    main()
    app.run()
