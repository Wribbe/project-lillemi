from lillemi import db

def test_ip_to_int():
  assert db.ip_to_int("0.0.0.1") == pow(256, 0)
  assert db.ip_to_int("0.0.1.0") == pow(256, 1)
  assert db.ip_to_int("0.1.0.0") == pow(256, 2)
  assert db.ip_to_int("1.0.0.0") == pow(256, 3)


def test_int_to_ip():
  assert db.int_to_ip(pow(256, 0)) == "0.0.0.1"
  assert db.int_to_ip(pow(256, 1)) == "0.0.1.0"
  assert db.int_to_ip(pow(256, 2)) == "0.1.0.0"
  assert db.int_to_ip(pow(256, 3)) == "1.0.0.0"


def test_ip_convertion():
  ip = "192.168.1.1"
  assert db.int_to_ip(db.ip_to_int(ip)) == ip


def test_user_get():
  name = "bananaman"
  secret = "12345"

  db.execute("INSERT INTO user (name,secret) VALUES (?,?);", (name, secret))
  db.commit()

  try:
    u = db.user_get(name)
    assert u
    assert u['name'] == name
    assert u['secret'] == secret
  finally:
    db.execute("DELETE FROM user WHERE name = (?);", (name,))
    db.commit()


def test_secret_set():
  name = "bananaman"
  secret = "12345"

  db.execute("INSERT INTO user (name,secret) VALUES (?,?);", (name, secret))
  db.commit()

  secret_changed = "changed_secret"

  db.secret_set(name, secret_changed)
  u = db.user_get(name)
  secret_in_db = u['secret']
  salt = db.salt_from_hash(secret_in_db)

  try:
    u = db.user_get(name)
    assert u['secret'] == db.secret_hash(secret_changed, salt=salt)
  finally:
    db.execute("DELETE FROM user WHERE name = (?);", (name,))
    db.commit()


def test_user_set():
  try:
    name = "user1"
    u = db.user_get(name)
    assert not u
    db.user_set(name, 'password')
    u = db.user_get(name)
    assert u
    assert u['name'] == name
  finally:
    db.execute("DELETE FROM user WHERE name = (?);", (name,))
    db.commit()


def test_user_auth():
  try:
    user = 'user_for_auth'
    password = 'password'
    db.user_set(user, password)
    db.commit()
    auth = db.user_auth(user, "wrong_password")
    assert not auth
    auth = db.user_auth(user, password)
    assert auth
    u = db.user_get(user)
    assert u['secret'] != password
  finally:
    db.execute("DELETE FROM user WHERE name = (?);", (user,))
    db.commit()
