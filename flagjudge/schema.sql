/* preloaded problems. detail is toml */
CREATE TABLE IF NOT EXISTS problem (id INT UNIQUE, title TEXT, detail TEXT, path TEXT);
/*
    submission status:
    0: judging
    1: accepted
    2: wrong answer
    3: time limit excceed
    4: output limit excceed
    5: runtime error
    6: compiler error
*/
CREATE TABLE IF NOT EXISTS submission (created_at INT, problem INT, language TEXT, code TEXT, flag TEXT , status INT);
CREATE TABLE IF NOT EXISTS judgelog (submission INT, judged_at INT, stdin TEXT, stdout TEXT, compiler_err TEXT);
