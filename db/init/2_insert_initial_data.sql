INSERT INTO USERS (name, hashed_password) VALUES ('六分儀ゲンドウ', 'ghaigfahdkfnaklhflaf');
INSERT INTO USERS (name, hashed_password) VALUES ('碇ユイ', 'ghailhgeighaihdafjl');
INSERT INTO USERS (name, hashed_password) VALUES ('当麻紗綾', 'higahghaihdafjl');

INSERT INTO CLASSES (name, semester, year) VALUES ('量子力学B', '前期', 2022);
INSERT INTO CLASSES (name, semester, year) VALUES ('物理科学課題演習B3', '前期', 2022);

INSERT INTO QUESTIONS(class_id, user_id, content, created_at) VALUES(1,1, '範囲はどのくらいですか？', NOW());
INSERT INTO QUESTIONS(class_id, user_id, content, created_at) VALUES(2,2, '何人で実験しますか？', NOW());

INSERT INTO ANSWERS(question_id, user_id, content, created_at) VALUES(1,2, '中心力場における3次元系までです。', NOW());
INSERT INTO ANSWERS(question_id, user_id, content, created_at) VALUES(1,3, 'JJサクライを読んでいるとわかりやすいです。', NOW());