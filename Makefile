SLYDS ?= slyds
PORT ?= 3000

.PHONY: site serve present new clean

# Build every talk into site/ with speaker notes stripped, plus the index page.
site:
	python3 scripts/build-site.py --slyds $(SLYDS)

# Preview the public site locally.
serve: site
	cd site && python3 -m http.server $(PORT)

# Present a talk with speaker notes: make present TALK=code-got-cheap
present:
	@test -n "$(TALK)" || (echo "usage: make present TALK=<folder>" && exit 1)
	$(SLYDS) serve $(TALK) -p $(PORT)

# Start a new talk: make new TITLE="My Talk" TALK=my-talk
new:
	@test -n "$(TITLE)" -a -n "$(TALK)" || (echo 'usage: make new TITLE="My Talk" TALK=my-talk' && exit 1)
	$(SLYDS) init "$(TITLE)" --dir $(TALK)
	printf 'title: %s\nsubtitle:\nevent:\ndate:\n' "$(TITLE)" > $(TALK)/talk.yaml

clean:
	rm -rf site */dist
