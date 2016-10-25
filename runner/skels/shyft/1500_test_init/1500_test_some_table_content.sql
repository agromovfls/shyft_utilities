INSERT INTO unittest_status
  SELECT
  '1500_test_init',
  'Test counts in aaa',
  COUNT(*) = 6,
  'Expected 6' FROM aaa;

INSERT INTO unittest_status
  SELECT
  '1500_test_init',
  'Test that have to fail',
  COUNT(*) = 5,
  'It doesn''t have an option to success' FROM aaa;

INSERT INTO unittest_status
  SELECT
  '1500_test_init',
  'New one happy test',
  1,
  'Expected 6' FROM aaa;