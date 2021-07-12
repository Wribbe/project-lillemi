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
