# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 14:07:56 2022

@author: kcruz29
"""

#Kevin Cruz
#CS 113


import urllib.request as url
import re

def get_addresses(content):
    '''Input can be either str type or bytes type from a urllib read'''
    #re package wants str type, not bytes
    strings = re.findall('[a-zA-Z0-9_.]*[@][a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', 
    str(content))
    
    #Some addresses have a trailing period. Need to get rid of it...
    for x in range(0, len(strings)):
        if strings[x].endswith("."):
            strings[x] = strings[x][0:len(strings[x])-1]
    return list(dict.fromkeys(strings)) # remove duplicates
           
def get_url(s):
    '''
    Returns a single link found in the argument s, which is a string of code
    found in a html file.
    '''
    href_tag = s.find('<a href=')
    
    if href_tag != -1:
        
        find_link = href_tag
        
        first_quote = s.find('"', find_link)
        second_quote = s.find('"', first_quote + 1)
    
        grab_link = s[first_quote + 1:second_quote]
        
        return grab_link
    
    else:
        return href_tag

def list_all_links(page):
    '''
    Returns all the links found in the argument pages, which is a string of 
    code found in a html file.
    ''' 
    list_container = []
    
    while '<a href="' in page:
        
        url = get_url(page)
        list_container.append(url)
        
        string = '<a href="' + url + '"'
        page = page.replace(string, 'found')
    
    return list_container

def crawl(start, limit):
    '''
    Returns a list of all the unique email addresses found, but it stop if you 
    have visited limit distinct web pages and return the list from that many 
    pages
    '''
    to_visit = [start]
    visited = []
    emails = []

    while to_visit:
        
        address = to_visit.pop()
        
        if address not in visited:
            content = url.urlopen(address).read()
            html = content.decode("UTF-8")
            decoded_address = get_addresses(html)
            
            links = list_all_links(html)
            
            visited.append(address)
            emails.extend(decoded_address)
            to_visit.extend(links)
            
            if len(visited) >= limit:
                break
            
    emails = set(emails)
    emails = list(emails)
    
    return emails        

#Website used for this program https://www.cs.uic.edu/~sloan/CS111Law/crawlerstart.html