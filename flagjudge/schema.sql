/* preloaded problems. detail is toml */
CREATE TABLE IF NOT EXISTS problem (id INT UNIQUE, title TEXT, detail TEXT, path TEXT);
/*
    submission status:
    0: judging
    1: accepted
    2: wrong answer
    3: time limit excceed
    4: output limit excceed (not implemented)
    5: runtime error
    6: compiler error
    7: other error
*/
CREATE TABLE IF NOT EXISTS submission (created_at NUM, problem INT, language TEXT, code TEXT, flag TEXT , status INT, visited INT);
CREATE TABLE IF NOT EXISTS judgelog (submission INT, judged_at NUM, stdin TEXT, stdout TEXT, stderr TEXT);
