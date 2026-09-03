"use server";

import { redirect } from "next/navigation";
import { revalidatePath } from "next/cache";
import { createClient } from "@/lib/supabase/server";

/** RLS ("borrar evaluaciones de mi empresa") ya restringe esto a la
 * propia empresa -- si el id no es tuyo, el delete simplemente no
 * afecta ninguna fila, sin necesidad de chequearlo acá primero. */
export async function deleteEvaluacion(id: string) {
  const supabase = await createClient();
  await supabase.from("evaluaciones").delete().eq("id", id);
  revalidatePath("/");
  redirect("/");
}
