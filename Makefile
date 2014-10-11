deploy:
	rake generate
	git add -f ./public
	git commit -m "regenerated website"
	git push origin deploy
	git push heroku deploy:master
	git checkout master
