install:
	wget https://quarto.org/download/latest/quarto-linux-amd64.deb
	sudo dpkg -i quarto-linux-amd64.deb
	quarto install extension quarto-ext/video
	quarto install extension sellorm/quarto-social-embeds

new-post:
	./scripts/new-post.sh
