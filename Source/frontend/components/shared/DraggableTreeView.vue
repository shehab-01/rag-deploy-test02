<template>
  <div class="draggable-tree">
    <draggable v-model="localItems" group="nested" :list="localItems" item-key="id" @change="emitUpdate">
      <template #item="{ element }">
        <div class="tree-node">
          <div class="tree-node-content" :class="{ 'is-active': isActive(element.id) }" @click="handleClick(element)">
            <v-icon v-if="element.children" class="mr-2">
              {{ isExpanded(element.id) ? 'mdi-folder-open' : 'mdi-folder' }}
            </v-icon>
            <v-icon v-else class="mr-2">mdi-file-document-outline</v-icon>
            <span>{{ element.title }}</span>
          </div>

          <div v-if="element.children && isExpanded(element.id)" class="pl-4">
            <draggable-tree-view
              :items="element.children"
              :active="active"
              @update:items="updateChildren(element, $event)"
              @click="$emit('click', $event)"
            />
          </div>
        </div>
      </template>
    </draggable>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import draggable from 'vuedraggable';

const props = defineProps<{
  items: any[];
  active?: string[];
}>();

const emit = defineEmits(['update:items', 'click']);

const expanded = ref(new Set([1])); // Start with root expanded
const localItems = computed({
  get: () => props.items,
  set: value => emit('update:items', value)
});

const isActive = (id: string | number) => props.active?.includes(id.toString());

const isExpanded = (id: number) => expanded.value.has(id);

const handleClick = (item: any) => {
  if (item.children) {
    if (expanded.value.has(item.id)) {
      expanded.value.delete(item.id);
    } else {
      expanded.value.add(item.id);
    }
  }
  emit('click', item);
};

const updateChildren = (parent: any, newChildren: any[]) => {
  const updatedItems = [...localItems.value];
  const updateNode = (items: any[], parentId: number): boolean => {
    for (let i = 0; i < items.length; i++) {
      if (items[i].id === parentId) {
        items[i].children = newChildren;
        return true;
      }
      if (items[i].children && updateNode(items[i].children, parentId)) {
        return true;
      }
    }
    return false;
  };

  updateNode(updatedItems, parent.id);
  emit('update:items', updatedItems);
};

const emitUpdate = () => {
  emit('update:items', localItems.value);
};
</script>

<style scoped>
.tree-node {
  padding: 2px 0;
}

.tree-node-content {
  display: flex;
  align-items: center;
  padding: 4px 8px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.tree-node-content:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.tree-node-content.is-active {
  background-color: var(--v-primary-base);
  color: white;
}

.draggable-tree {
  width: 100%;
}
</style>
