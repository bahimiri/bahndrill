import type { Line } from '@/types/lines.ts'

export const isUBahn = ({ name }: Line) => name.startsWith('U')
export const isSBahn = ({ name }: Line) => name.startsWith('S')
