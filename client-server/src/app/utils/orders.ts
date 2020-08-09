export class orderUtils {

    // arbitrary numbers to facilitate the status' sort order 
    static DECLINED_PRECEDENCE = 2000;
    static NEW_PRECEDENCE = 1000;
    static IN_PROGRESS_PRECEDENCE = 500;
    static COMPLETED_PRECEDENCE = 0;
    static BUGGED_PRECEDENCE = 5000;
    

    static isCompleted(order): boolean{
        return order.send_tstmp && order.accept_tstmp && order.complete_tstmp;
    }

    static isInProgress(order): boolean{
        return order.send_tstmp && order.accept_tstmp && !order.complete_tstmp;
    }
    
    static isNew(order): boolean{
        return order.send_tstmp && !order.accept_tstmp && !order.complete_tstmp;
    }

    static isDeclined(order): boolean{
        return order.is_cancelled;
    }

    // sort by precedence: Bugged status, Cancelled, New, In Progress, Completed
    static statusToPrecedence(order): number{
        if(orderUtils.isNew(order)){
            return orderUtils.NEW_PRECEDENCE;
        }
        else if(orderUtils.isInProgress(order)){
            return orderUtils.IN_PROGRESS_PRECEDENCE;
        }
        else if(orderUtils.isCompleted(order)){
            return orderUtils.COMPLETED_PRECEDENCE;
        }
        else if(orderUtils.isDeclined(order)){
            return orderUtils.DECLINED_PRECEDENCE;
        }
        // in case of some weird status scenario, pull it to the top so it is visible
        console.warn("The order: " + order.toString() + "is neither New, In Progress, nor Completed, OH NO!");
        return orderUtils.BUGGED_PRECEDENCE;
    }
    // sorts statuses by order prefer
    static OrderStatusComparator(ord1: any, ord2: any): number{
        let precedence1 = orderUtils.statusToPrecedence(ord1);
        let precedence2 = orderUtils.statusToPrecedence(ord2);
        return precedence2 - precedence1;
    }
}