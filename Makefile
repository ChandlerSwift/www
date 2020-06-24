dev-server:
	docker build -t jekyll-dev-server . ; docker run -it -p4000:4000 --mount type=bind,source=`pwd`,destination=/src jekyll-dev-server serve --host 0.0.0.0 --incremental

.PHONY: clean
clean:
	rm -rf .jekyll-cache .jekyll-metadata
