import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import argparse

target_url = 'https://en.wikipedia.org/wiki/Philosophy'

filter_list = ['/wiki/File:',
                '/wiki/Wikipedia:',
                '/wiki/Category:',
                '/wiki/Help:',
                '/wiki/Template:',
                '/wiki/Talk:',
                '/wiki/Portal:',
                '/wiki/Special:',
                '/wiki/Project:']
visited = []

def extract_links(url):
    res = requests.get(url, timeout=1)
    soup = BeautifulSoup(res.text, "html.parser")
    base = url
    links = []
    for link in soup.find_all("a"):
        href = link.get('href')
        if filter_link(href):
            links.append(urljoin(base, href))
    return links

def filter_link(link):
    if not link:
        return False
    if not link.startswith('/wiki/') or link.endswith('_(disambiguation)'):
        return False
    return all(not link.startswith(s) for s in filter_list)
    

def bfs_traverse(start = '', target_url = target_url, depth = 0, max_depth = 10):

    queue = []
    queue.append([start, start])
    # append None for correct depth calculation 
    queue.append(None)

    while queue or depth < max_depth:
        node = queue.pop(0)

        if not node:
            depth += 1
            continue

        url = node[0]
        path = node[1]
        
        if url in visited:
            continue
        
        if depth > max_depth:
            print(f'Reached maximum depth of {max_depth}')
            return
        

        time.sleep(.5)
        print(f'parsing page {url}')
        links = extract_links(url)
        if target_url in links:
            print(f'FOUND PHILOSOPHY PAGE @ depth of {depth}')
            path +=  '  ---->   ' + target_url
            print(f'Path is {path}')
            return True
        
        visited.append(url)
        for link in links:
            if link in visited:
                # print(f'visited already {link}')
                continue
            else:
                queue.append([link, path + '  ---->  ' + link])

        # append None at the end of each level to keep track of depth
        queue.append(None)
    
    
def dfs_traverse(start = '', trace = '', target_url = target_url, depth = 0, max_depth = 10):
    
    print(f'parsing {start}')
    if start in visited:
        # print('already visited')
        return
        
    if depth > max_depth:
        print(f'Reached maximum depth of {max_depth}')
        # print(f'trace is {trace}')
        return

    links = extract_links(start)
    if target_url in links:
        print(f'FOUND PHILOSOPHY PAGE @ depth of {depth}')
        print(trace + '   ---->   ' + target_url)
        return True
    else:
        visited.append(start)
        for link in links:
            time.sleep(.5)
            dfs_traverse(link, trace = trace + '   ---->   ' + link, depth=depth+1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', action = 'store', dest = 'url', default = 'https://en.wikipedia.org/wiki/Special:Random')
    parser.add_argument('--alg', action = 'store', dest = 'alg', default = 'bfs')
    args = parser.parse_args()

    if args.alg == 'bfs':
        bfs_traverse(args.url)
    else:
        dfs_traverse(args.url)
        
# url = 'https://en.wikipedia.org/wiki/Mathematics'
# url = 'https://en.wikipedia.org/wiki/Aristotle'
