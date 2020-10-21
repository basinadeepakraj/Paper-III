#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 11:18:46 2019

@author: basina
"""

class Node:
    def __init__(self, identity, key, choiceindx):
        self.next = None
        self.identity = identity
        self.key = key
        self.choiceindx = choiceindx

class ApplianceSSLL:
    def __init__(self, identity= -1, key=-1, choiceindx=-1):
        self.head = Node(identity, key, choiceindx)
        self.tail = Node(identity, key, choiceindx)

    def tail_insert(self, identity, key,  choiceindx):
        if self.head.next is None:
            self.head.next = Node(identity, key, choiceindx)
            self.tail = self.head.next
        else:
            self.tail.next = Node(identity, key, choiceindx)
            self.tail = self.tail.next



    def insert(self, identity, key, choiceindx):
        current = self.head
        if current.next is None:
            current.next = Node(identity, key, choiceindx)
            return
        while current.next is not None:
            if current.next.key < key:
                break
            else:
                current = current.next
        if current.next is None:
            # Indicates end of the list
            current.next = Node(identity, key, choiceindx)
        else:
            # Found a place to insert
            t = Node(identity, key, choiceindx)
            t.next = current.next
            current.next = t

    def pop(self):
        if self.head.next is None:
            print ("List Empty")
            return
        else:
            identity = self.head.next.identity
            key = self.head.next.key
            choiceindx = self.head.next.choiceindx
            self.head.next = self.head.next.next
            return identity, key, choiceindx

    def isempty(self):
        if self.head.next is None:
            return True
        else:
            return False
            
    def isnotempty(self):
        if self.head.next is None:
            return False
        else:
            return True

    def printls(self):
        current = self.head.next
        while current is not None:
            if current.identity is not None:
                print("id:",current.identity)
            current = current.next

