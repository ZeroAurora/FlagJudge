# FlagJudge

Code in, flag out. The poorest online judge for use with CTF-like contests.

Almost done.

## Use cases

Judge code and give flag to those who answered the problem correctly.

Intended for use in ZFun High School Student Computer Skill Contest.

The templates are in Chinese but that's fine. Just fork and translate it as needed.

## Deployment

1. Deploy [Piston](https://github.com/engineer-man/piston) and edit `data/languages.toml` and `config.toml`.
2. `docker build . --tag flagjudge`
3. `docker run -it -v $PWD/data:/usr/src/app/data -v $PWD/config.toml:/usr/src/app/config.toml --network host flagjudge`
4. Visit `ip:8000`

## Why the name

1. This is for use with CTFs.
2. Shitcoded. Vulnerable. Don't hide flags in the codebase. Others will find them out.

## License

[GLWTPL](./GLWTPL). Good luck.

Also dual licensed under [UNLICENSE](./UNLICENSE) if you need a OSI-approved public domain license.
