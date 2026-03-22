window.HELP_IMPROVE_VIDEOJS = false;

function copyBibTeX() {
    const bibtexElement = document.getElementById('bibtex-code');
    const button = document.querySelector('.copy-bibtex-btn');
    if (!bibtexElement || !button) return;

    const copyText = button.querySelector('.copy-text');

    navigator.clipboard.writeText(bibtexElement.textContent).then(function() {
        button.classList.add('copied');
        if (copyText) copyText.textContent = 'Cop';

        setTimeout(function() {
            button.classList.remove('copied');
            if (copyText) copyText.textContent = 'Copy';
        }, 2000);
    }).catch(function(err) {
        console.error('Failed to copy: ', err);
        const textArea = document.createElement('textarea');
        textArea.value = bibtexElement.textContent;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);

        button.classList.add('copied');
        if (copyText) copyText.textContent = 'Cop';
        setTimeout(function() {
            button.classList.remove('copied');
            if (copyText) copyText.textContent = 'Copy';
        }, 2000);
    });
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

window.addEventListener('scroll', function() {
    const scrollButton = document.querySelector('.scroll-to-top');
    if (!scrollButton) return;
    if (window.pageYOffset > 300) {
        scrollButton.classList.add('visible');
    } else {
        scrollButton.classList.remove('visible');
    }
});

function initVideoScrollStrip() {
    const strip = document.getElementById('videoScrollStrip');
    if (!strip) return;

    const slides = strip.querySelectorAll('.video-scroll-slide');
    const videos = strip.querySelectorAll('video');
    const prevBtn = document.querySelector('.video-scroll-prev');
    const nextBtn = document.querySelector('.video-scroll-next');
    const dots = document.querySelectorAll('.video-scroll-dot');

    if (slides.length === 0) return;

    function getScrollIndex() {
        const w = slides[0].offsetWidth;
        if (!w) return 0;
        return Math.min(
            slides.length - 1,
            Math.max(0, Math.round(strip.scrollLeft / w))
        );
    }

    function syncDots(activeIdx) {
        dots.forEach(function(d, j) {
            var on = j === activeIdx;
            d.classList.toggle('is-active', on);
            if (on) {
                d.setAttribute('aria-current', 'true');
            } else {
                d.removeAttribute('aria-current');
            }
        });
    }

    function pauseOthers(activeIdx) {
        videos.forEach(function(v, j) {
            if (j !== activeIdx) {
                v.pause();
            }
        });
    }

    function goTo(index) {
        var i = Math.max(0, Math.min(slides.length - 1, index));
        var target = slides[i];
        strip.scrollTo({
            left: target.offsetLeft,
            behavior: 'smooth'
        });
        syncDots(i);
        pauseOthers(i);
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            goTo(getScrollIndex() - 1);
        });
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            goTo(getScrollIndex() + 1);
        });
    }

    dots.forEach(function(dot) {
        dot.addEventListener('click', function() {
            var i = parseInt(dot.getAttribute('data-index'), 10);
            if (!isNaN(i)) goTo(i);
        });
    });

    var scrollTimer = null;
    strip.addEventListener('scroll', function() {
        if (scrollTimer) window.clearTimeout(scrollTimer);
        scrollTimer = window.setTimeout(function() {
            syncDots(getScrollIndex());
        }, 50);
    }, { passive: true });

    strip.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            e.preventDefault();
            goTo(getScrollIndex() - 1);
        } else if (e.key === 'ArrowRight') {
            e.preventDefault();
            goTo(getScrollIndex() + 1);
        }
    });

    window.addEventListener('resize', function() {
        syncDots(getScrollIndex());
    });
}

function initRevealOnScroll() {
    var els = document.querySelectorAll('.reveal-on-scroll');
    if (els.length === 0) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        els.forEach(function(el) {
            el.classList.add('is-revealed');
        });
        return;
    }

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-revealed');
            }
        });
    }, {
        threshold: 0.08,
        rootMargin: '0px 0px -8% 0px'
    });

    els.forEach(function(el) {
        observer.observe(el);
    });
}

function initPaperToc() {
    var toc = document.getElementById('paperToc');
    if (!toc) return;

    var links = toc.querySelectorAll('.paper-toc-link');
    var sectionIds = ['paper-intro', 'paper-related', 'paper-method', 'paper-experiments', 'paper-conclusion', 'paper-ack'];

    function setActive(id) {
        links.forEach(function(a) {
            var t = a.getAttribute('data-paper-target');
            a.classList.toggle('is-active', t === id);
        });
    }

    function syncFromScroll() {
        var centerY = window.innerHeight * 0.38;
        var bestId = sectionIds[0];
        var bestScore = Infinity;

        sectionIds.forEach(function(id) {
            var el = document.getElementById(id);
            if (!el) return;
            var r = el.getBoundingClientRect();
            if (r.bottom < 0 || r.top > window.innerHeight) return;
            var mid = (r.top + r.bottom) / 2;
            var score = Math.abs(mid - centerY);
            if (score < bestScore) {
                bestScore = score;
                bestId = id;
            }
        });
        setActive(bestId);
    }

    var ticking = false;
    window.addEventListener('scroll', function() {
        if (!ticking) {
            window.requestAnimationFrame(function() {
                syncFromScroll();
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });

    links.forEach(function(a) {
        a.addEventListener('click', function(e) {
            e.preventDefault();
            var id = a.getAttribute('data-paper-target');
            var el = document.getElementById(id);
            if (!el) return;
            el.open = true;
            el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            if (history.replaceState) {
                history.replaceState(null, '', '#' + id);
            }
            setActive(id);
        });
    });

    sectionIds.forEach(function(id) {
        var el = document.getElementById(id);
        if (el) {
            el.addEventListener('toggle', function() {
                if (el.open) {
                    setActive(id);
                }
            });
        }
    });

    if (location.hash) {
        var h = location.hash.slice(1);
        var target = document.getElementById(h);
        if (target && target.tagName === 'DETAILS') {
            target.open = true;
            window.setTimeout(function() {
                target.scrollIntoView({ block: 'start' });
                setActive(h);
            }, 80);
        }
    } else {
        syncFromScroll();
    }
}

function typesetPaperFoldBodies(nodes) {
    if (!window.MathJax || !MathJax.typesetPromise) {
        return Promise.resolve();
    }
    var list = nodes || document.querySelectorAll('.paper-fold-body');
    return MathJax.typesetPromise(list).catch(function() {});
}

function initMathJaxPaper() {
    var script = document.getElementById('MathJax-script');
    function runTypeset() {
        typesetPaperFoldBodies();
    }
    if (window.MathJax && MathJax.typesetPromise) {
        runTypeset();
    } else if (script) {
        script.addEventListener('load', runTypeset);
    }
    document.querySelectorAll('details.paper-fold').forEach(function(d) {
        d.addEventListener('toggle', function() {
            if (d.open) {
                var body = d.querySelector('.paper-fold-body');
                if (body) {
                    typesetPaperFoldBodies([body]);
                }
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    initVideoScrollStrip();
    initRevealOnScroll();
    initPaperToc();
    initMathJaxPaper();
});
